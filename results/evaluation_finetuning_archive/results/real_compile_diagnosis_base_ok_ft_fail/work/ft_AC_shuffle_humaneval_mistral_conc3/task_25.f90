program factorize_demo
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the factorize function
  call factorize(n, factors)
  
  ! Output the result
  print *, factors
  
contains

  subroutine factorize(n, factors)
    implicit none
    integer, intent(in) :: n
    integer, intent(out) :: factors(:)
    integer :: i, count
    integer, allocatable :: temp(:)
    
    ! Allocate temporary array for factors
    allocate(temp(n))
    count = 0
    
    ! Find prime factors
    do i = 2, n
      if (mod(n, i) == 0) then
        do while (mod(n, i) == 0)
          count = count + 1
          temp(count) = i
          n = n / i
        end do
      end if
      if (n == 1) exit
    end do
    
    ! Allocate final factors array
    allocate(factors(count))
    factors = temp(1:count)
    
    deallocate(temp)
  end subroutine factorize

end program factorize_demo