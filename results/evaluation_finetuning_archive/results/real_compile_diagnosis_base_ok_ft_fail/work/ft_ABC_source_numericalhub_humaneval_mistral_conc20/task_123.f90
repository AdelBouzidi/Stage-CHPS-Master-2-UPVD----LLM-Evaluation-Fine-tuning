program test_odd_collatz
  implicit none
  integer, parameter :: i4b = selected_int_kind(9)
  integer(i4b) :: n
  integer(i4b), allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  result = get_odd_collatz(n)
  
  ! Sort the result
  call sort(result)
  
  ! Output result
  print *, result
contains

  function get_odd_collatz(n) result(res)
    implicit none
    integer(i4b), intent(in) :: n
    integer(i4b), allocatable :: res(:)
    integer(i4b) :: temp
    
    res = []
    temp = n
    do
      if (mod(temp, 2) == 1) then
        if (allocated(res)) then
          res = [res, temp]
        else
          allocate(res(1))
          res(1) = temp
        end if
      end if
      if (temp == 1) exit
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
  end function get_odd_collatz

  subroutine sort(arr)
    implicit none
    integer(i4b), intent(inout) :: arr(:)
    integer(i4b) :: i, j, temp
    do i = 1, size(arr) - 1
      do j = i + 1, size(arr)
        if (arr(j) < arr(i)) then
          temp = arr(i)
          arr(i) = arr(j)
          arr(j) = temp
        end if
      end do
    end do
  end subroutine sort

end program test_odd_collatz