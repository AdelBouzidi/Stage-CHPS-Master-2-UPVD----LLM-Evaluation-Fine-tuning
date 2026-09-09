program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  call f(n, result)
  
  ! Print output
  print *, result
contains

  subroutine f(n, result)
    implicit none
    integer, intent(in) :: n
    integer, intent(out) :: result(n)
    integer :: i
    integer :: sum_val
    integer :: fact_val
    integer :: j
    
    do i = 1, n
      if (mod(i, 2) == 0) then
        ! Even index: factorial
        fact_val = 1
        do j = 1, i
          fact_val = fact_val * j
        end do
        result(i) = fact_val
      else
        ! Odd index: sum from 1 to i
        sum_val = 0
        do j = 1, i
          sum_val = sum_val + j
        end do
        result(i) = sum_val
      end if
    end do
  end subroutine f

end program main