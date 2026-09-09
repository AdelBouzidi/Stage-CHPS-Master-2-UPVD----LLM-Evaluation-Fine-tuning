program rescale_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: n
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: result(:)
  integer :: i

  ! Read input
  read(*,*) n
  allocate(numbers(n))
  read(*,*) numbers

  ! Call the rescale function
  call rescale_to_unit(n, numbers, result)

  ! Output result
  write(*,*) result

contains

  subroutine rescale_to_unit(n, numbers, result)
    implicit none
    integer, intent(in) :: n
    real(dp), intent(in) :: numbers(n)
    real(dp), intent(out) :: result(n)
    real(dp) :: min_val, max_val
    integer :: i

    min_val = numbers(1)
    max_val = numbers(1)
    do i = 2, n
      if (numbers(i) < min_val) min_val = numbers(i)
      if (numbers(i) > max_val) max_val = numbers(i)
    end do

    if (max_val == min_val) then
      result = 0.0_dp
    else
      result = (numbers - min_val) / (max_val - min_val)
    end if
  end subroutine rescale_to_unit

end program rescale_demo