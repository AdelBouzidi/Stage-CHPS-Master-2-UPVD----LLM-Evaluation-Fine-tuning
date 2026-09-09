program factorize_demo
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  
  ! Read input
  read(*,*) n
  
  ! Call factorize function
  call factorize(n, factors)
  
  ! Print output
  print *, factors
  
contains

  subroutine factorize(n, factors)
    implicit none
    integer, intent(in) :: n
    integer, intent(out), allocatable :: factors(:)
    integer :: i, count
    integer, allocatable :: temp(:)
    
    ! Initialize factors array
    allocate(temp(1))
    temp(1) = 1
    count = 1
    
    ! Find prime factors
    do i = 2, n
      if (mod(n, i) == 0) then
        count = 0
        do while (mod(n, i) == 0)
          count = count + 1
          n = n / i
        end do
        allocate(temp(count))
        temp(1:count) = i
        factors = temp
        exit
      end if
    end do
    
    ! If n > 1, it's a prime factor
    if (n > 1) then
      allocate(temp(1))
      temp(1) = n
      factors = temp
    end if
    
    deallocate(temp)
  end subroutine factorize

end program factorize_demo