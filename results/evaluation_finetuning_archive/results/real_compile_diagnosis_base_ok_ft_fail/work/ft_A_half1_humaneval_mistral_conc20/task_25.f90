program factorize_demo
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the factorize function
  call factorize(n, factors)
  
  ! Print output
  print *, factors
contains

  subroutine factorize(n, factors)
    implicit none
    integer, intent(in) :: n
    integer, intent(out) :: factors(:)
    integer :: i, count
    integer, allocatable :: temp(:)
    
    ! Initialize factors array
    count = 0
    do i = 2, n
      if (mod(n, i) == 0) then
        count = count + 1
      end if
    end do
    
    allocate(factors(count))
    i = 1
    do while (n > 1)
      if (mod(n, i) == 0) then
        factors(i) = i
        n = n / i
      else
        i = i + 1
      end if
    end do
  end subroutine factorize

end program factorize_demo